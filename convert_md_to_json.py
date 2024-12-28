import glob
from markdown_converter.markdown_converter import MarkdownConverter

"""
Author: Tariq Ahmed
Email: t.ahmed@stride.ae
Organization: Stride Information Technology

This script converts markdown files to JSON and optionally saves the output to a database.
"""

def main():
    """
    Main function to convert markdown files to JSON and optionally save the output to a database.

    This function runs two scenarios:
    1. Saving in both local folder and database
    2. Saving only in local folder using only the file with name: "convert_test.md"
    """
    # Scenario 1: Saving in both local folder and  database
    converter1 = MarkdownConverter('example/convert_test.md', save_to_db=True)
    output_file1 = converter1.convert()
    print(f'Scenario 1: JSON file has been created successfully: {output_file1}')

    # Scenario 2: Saving only in local folder
    converter2 = MarkdownConverter('example/convert_test.md')
    output_file2 = converter2.convert()
    print(f'Scenario 2: JSON file has been created successfully: {output_file2}')

    md_files = glob.glob('example/*.md')
    for md_file in md_files:
        output_file = None
        try:
            print(f"\nProcessing {md_file}")
            converter = MarkdownConverter(md_file)
            output_file = converter.convert()
            print(f'JSON file has been created successfully: {output_file}')
            print(f'JSON file {output_file} is valid.')

        except Exception as e:
            print(f"Error processing {md_file}: {str(e)}")

if __name__ == '__main__':
    main()
