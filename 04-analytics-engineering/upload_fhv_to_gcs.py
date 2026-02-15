"""
Download FHV taxi data from DataTalksClub GitHub release,
decompress from .csv.gz, and upload as .csv to a GCS bucket.

Prerequisites:
    pip install google-cloud-storage requests

Usage:
    python upload_fhv_to_gcs.py
"""

import argparse
import gzip
import logging
import shutil
import tempfile
from pathlib import Path

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/repos/DataTalksClub/nyc-tlc-data/releases/tags/fhv"


def get_asset_urls(github_token: str | None = None) -> list[dict]:
    """Fetch the list of release assets from the GitHub API."""
    headers = {"Accept": "application/vnd.github+json"}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    resp = requests.get(GITHUB_API_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    release = resp.json()

    assets = []
    for asset in release.get("assets", []):
        name = asset["name"]
        if not name.endswith(".csv.gz"):
            continue
        assets.append({
            "name": name,
            "csv_name": name.removesuffix(".gz"),  # fhv_tripdata_2019-01.csv
            "url": asset["browser_download_url"],
            "size_mb": round(asset["size"] / (1024 * 1024), 1),
        })

    log.info(f"Found {len(assets)} .csv.gz assets in the release")
    return assets


def download_decompress_upload(
    asset: dict,
    bucket: storage.Bucket,
    prefix: str,
    tmp_dir: str,
) -> str:
    """Download .csv.gz, decompress to temp file, upload .csv to GCS."""
    blob_name = f"{prefix}{asset['csv_name']}"
    blob = bucket.blob(blob_name)

    # Skip if already uploaded (idempotent re-runs)
    if blob.exists():
        log.info(f"SKIP {asset['csv_name']} — already exists at gs://{bucket.name}/{blob_name}")
        return blob_name

    gz_path = Path(tmp_dir) / asset["name"]
    csv_path = Path(tmp_dir) / asset["csv_name"]

    try:
        # 1. Download .csv.gz
        log.info(f"Downloading {asset['name']} ({asset['size_mb']} MB compressed) ...")
        with requests.get(asset["url"], stream=True, timeout=600) as resp:
            resp.raise_for_status()
            with open(gz_path, "wb") as f:
                shutil.copyfileobj(resp.raw, f)

        # 2. Decompress
        log.info(f"Decompressing {asset['name']} ...")
        with gzip.open(gz_path, "rb") as f_in, open(csv_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

        # Remove .gz to free disk space before upload
        gz_path.unlink()

        csv_size_mb = csv_path.stat().st_size / (1024 * 1024)
        log.info(f"Uploading {asset['csv_name']} ({csv_size_mb:.1f} MB decompressed) ...")

        # 3. Upload .csv
        blob.upload_from_filename(str(csv_path), content_type="text/csv", timeout=600)

        log.info(f"Done: gs://{bucket.name}/{blob_name}")
        return blob_name

    finally:
        # Clean up temp files regardless of success/failure
        gz_path.unlink(missing_ok=True)
        csv_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(
        description="Download FHV taxi data from GitHub and upload as CSV to GCS"
    )
    parser.add_argument("--bucket", default="module_04_zoomcamp", help="GCS bucket name")
    parser.add_argument("--prefix", default="raw/fhv/", help="GCS prefix (folder). Default: raw/fhv/")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers. Default: 4")
    parser.add_argument("--github-token", default=None, help="GitHub PAT (optional, avoids rate limits)")
    args = parser.parse_args()

    prefix = args.prefix if args.prefix.endswith("/") else args.prefix + "/"

    # 1. Discover assets
    assets = get_asset_urls(args.github_token)
    if not assets:
        log.error("No assets found. Check the GitHub release or your network.")
        return

    total_mb = sum(a["size_mb"] for a in assets)
    log.info(f"Total compressed download: ~{total_mb:.0f} MB across {len(assets)} files")

    # 2. Set up GCS
    credentials_path = Path(__file__).parent / "dbt_zoomcamp.json"
    if not credentials_path.exists():
        log.error(f"Credentials file not found: {credentials_path}")
        return
    client = storage.Client.from_service_account_json(str(credentials_path))
    bucket = client.bucket(args.bucket)
    if not bucket.exists():
        log.error(f"Bucket gs://{args.bucket} does not exist. Create it first.")
        return

    # 3. Download, decompress, upload in parallel
    succeeded = []
    failed = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_asset = {
                executor.submit(
                    download_decompress_upload, asset, bucket, prefix, tmp_dir
                ): asset
                for asset in assets
            }

            for future in as_completed(future_to_asset):
                asset = future_to_asset[future]
                try:
                    blob_name = future.result()
                    succeeded.append(blob_name)
                except Exception as e:
                    log.error(f"FAILED {asset['name']}: {e}")
                    failed.append(asset["name"])

    # 4. Summary
    log.info(f"\nDone. {len(succeeded)} succeeded, {len(failed)} failed.")
    if failed:
        log.warning(f"Failed files: {failed}")


if __name__ == "__main__":
    main()