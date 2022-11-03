import os
import argparse
import csv 
import json
import hashlib
import pandas as pd


INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .csv file."
INVALID_PATH_MSG = "Error: Invalid file/path name. Path %s does not exist."

def validate_file(file_name):
    if not valid_filetype(file_name):
        print(INVALID_PATH_MSG%(file_name))
        print("Please try again")
        quit()
    return

def valid_filetype(file_name):
    return file_name.endswith('.csv')

def valid_path(path):
    return os.path.exists(path)

def main():
    # Create parser object
    parser = argparse.ArgumentParser(description='Process your CSV file here and get the required output')
    
    # Defining argument(s)
    parser.add_argument("file", type=str, nargs=1, help="Reads your NFT csv file, generates the json files for each NFT, hashes them, then returns an updated CSV.",
    metavar="file_name", default=None)

    args = parser.parse_args()

    if args.file != None:
        validate_file(args.file[0])
        file_name = args.file[0]
        print(file_name)

    hash_list = []

    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            series_number = row[0]
            filename = row[1]
            name= row[2]
            description= row[3]
            gender = row[4]
            attributes = row[5]
            uuid = row[6]

            # response model 
            nft = {
                "format": "CHIP-0007",
                "name": name,
                "description": description,
                "minting_tool": "Team x",
                "sensitive_content": False,
                "series_number": series_number,
                "series_total": 420,
                "attributes": [
                    {
                        "trait_type": "gender",
                        "value": gender
                    }
                ],
                "collection": {
                    "name": "Zuri NFT tickets for free lunch",
                    "id": uuid,
                    "attributes": [
                        {
                            "type": "description",
                            "value": "Rewards for accomplishments during HNGi9"
                        }
                    ]
                },
            }

            # Dump each nft entry on its own '.json' file
            with open("{}.json".format(filename), 'w') as outputfile:
                json.dump(nft, outputfile, indent=4, separators=(", ", ": "))
                outputfile.close()

            # Prevents the script from unintentional hashing
            if filename == "Filename":
                pass

            else:
                with open("{}.json".format(filename), "rb") as f:
                    bytes = f.read()
                    readable_hash = hashlib.sha256(bytes).hexdigest()
                    hash_list.append(readable_hash)
                    f.close()
        
        # The appended generated sha256 hash values for each nft file is to respective rows in the original csv file.
        csv_input = pd.read_csv(file_name)
        csv_input['Hash'] = hash_list
    
        csv_input.to_csv('filename.output.csv', index=False)


if __name__ == "__main__":
    main()


        