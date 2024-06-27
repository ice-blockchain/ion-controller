#!/bin/bash

# Function to show usage
show_help() {
    echo "Usage: $0 -u <url> -o <output_file>"
    echo "Download global.config.json from a given URL."
    echo "  -u URL            The URL to download the config from."
    echo "  -o OUTPUT_FILE    The file to save the downloaded config."
    exit 1
}

# Check if at least 2 arguments are provided
if [ $# -lt 4 ]; then
    show_help
fi

# Parse command-line arguments
while getopts "u:o:h" opt; do
    case ${opt} in
        u )
            url=$OPTARG
            ;;
        o )
            output_file=$OPTARG
            ;;
        h )
            show_help
            ;;
        \? )
            show_help
            ;;
    esac
done

# Check if url and output_file variables are set
if [ -z "${url}" ] || [ -z "${output_file}" ]; then
    show_help
fi

# Download the file using wget
echo "Downloading ${url} to ${output_file}..."
wget -O "${output_file}" "${url}"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Download completed successfully."
else
    echo "Failed to download the file."
    exit 1
fi
