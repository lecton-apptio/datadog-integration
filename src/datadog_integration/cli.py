"""Command-line interface for Datadog key validation."""

import json
import os
from typing import Optional

from datadog_integration.core import DatadogValidator, load_env_file


def get_optional_env(*names: str) -> Optional[str]:
    """Get the first available environment variable from a list of names.

    Args:
        *names: Variable names to check in order

    Returns:
        The first non-empty value found, or None
    """
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def print_section(title: str) -> None:
    """Print a section header.

    Args:
        title: The section title
    """
    print(f"\n=== {title} ===")


def main() -> None:
    """Main CLI entry point."""
    load_env_file()

    api_key_name = get_optional_env("DD_API_KEY_NAME")
    api_key = get_optional_env("DD_API_KEY")
    app_key_name = get_optional_env("DD_APP_KEY_NAME")
    app_key = get_optional_env("DD_APP_KEY", "DD_APPLICATION_KEY")
    app_key_id = get_optional_env("DD_KEY_ID", "DD_APP_ID")
    site = os.getenv("DD_SITE", "datadoghq.com").strip()

    validator = DatadogValidator(
        api_key=api_key,
        app_key=app_key,
        site=site,
        api_key_name=api_key_name,
        app_key_name=app_key_name,
        app_key_id=app_key_id,
    )

    print_section("Configured credentials")
    print(json.dumps(validator.get_config_summary(), indent=2))

    if api_key:
        print_section("API key validation")
        api_validation = validator.validate_api_key()
        if api_validation:
            print(json.dumps(api_validation.to_dict(), indent=2))
    else:
        print_section("API key validation")
        print("DD_API_KEY not set, so API key validation was skipped.")

    if not app_key:
        print_section("App key / permissions")
        print(
            "DD_APP_KEY or DD_APPLICATION_KEY not set, so permission/scope inspection was skipped."
        )
        return

    if not api_key:
        print_section("App key / permissions")
        print(json.dumps(validator.get_missing_api_key_error(), indent=2))
        return

    print_section("Dashboards read test")
    dashboards_read = validator.test_dashboards_read()
    if dashboards_read:
        print(json.dumps(dashboards_read.to_dict(), indent=2))

    print_section("Metrics read test")
    metrics_read = validator.test_metrics_read()
    if metrics_read:
        print(json.dumps(metrics_read.to_dict(), indent=2))

    print_section("Notes")
    print(
        "- DD_API_KEY is optional only if you want a config sanity check, but it is required for live Datadog API requests.\n"
        "- DD_APP_KEY / DD_APPLICATION_KEY should contain the application key secret.\n"
        "- DD_KEY_ID / DD_APP_ID can contain the application key identifier used to fetch that key's metadata.\n"
        "- Each API result now includes a redacted curl command you can paste into a ticket as evidence.\n"
        "- This script now validates granted read scopes using dashboard and metrics read-only endpoints."
    )


if __name__ == "__main__":
    main()

# Made with Bob
