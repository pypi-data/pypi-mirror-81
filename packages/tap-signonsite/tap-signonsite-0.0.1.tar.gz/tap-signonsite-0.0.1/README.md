# tap-signonsite

This is a [Singer](https://singer.io) tap that produces JSON-formatted
data from the SignOnSite API following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from the [SignOnSite API](https://support.signonsite.com.au/en/articles/4209421-api)
- Extracts the following resources from SignOnSite:
  - Sites
  - Attendances
  - Companies
  - Users
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Quick start

1. Install

   We recommend using a virtualenv:

   ```bash
   > virtualenv -p python3 venv
   > source venv/bin/activate
   > pip install -e .
   ```

2. Get your SignOnSite API key

   Log into the [SignOnSite portal](https://app.signonsite.com.au/login) with an admin account, and go to the [settings page](https://app.signonsite.com.au/companies/5084/settings). Click on the button at the bottom to generate the secret API key.

3. Create the config file

   Create a JSON file called `config.json` containing the access token you just created.

   ```json
   { "api_key": "yourapikey" }
   ```

4. Run the tap in discovery mode to get properties.json file

   ```bash
   tap-signonsite --config config.json --discover > properties.json
   ```

5. In the properties.json file, select the streams to sync

   Each stream in the properties.json file has a "schema" entry. To select a stream to sync, add `"selected": true` to that stream's "schema" entry. For example, to sync the pull_requests stream:

   ```
   ...
   "tap_stream_id": "sites",
   "schema": {
     "selected": true,
     "properties": {
   ...
   ```

6. Run the application

   `tap-signonsite` can be run with:

   ```bash
   tap-signonsite --config config.json --properties properties.json
   ```
   
   Copyright &copy; 2020 Stitch
