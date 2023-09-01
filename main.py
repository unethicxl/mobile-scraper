import json
import os
from scraper import Model

def main():
    devices = []
    for i in range(1, 5):
        try:
            models = Model.scrape_models(i)
            for model in models.values():
                try:
                    Model.fill_data(model)
                    
                    devices.append(model.__dict__)
                    with open("devices.json", "w") as f:
                        json.dump(devices, f, indent="\t")
                    # print(devices)
                except Exception as e:
                    print(f"Error processing model: {e}")
        except Exception as e:
            print(e)
            break
    
    

if __name__ == "__main__":
    main()
