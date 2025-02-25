import os
import csv
import subprocess

def clone_repos_from_csv(csv_file: str, data_path: str):
    """
    Liest eine CSV-Datei ein und klont die in jeder Zeile angegebenen GitHub-Repos in den angegebenen Ordner.

    Args:
        csv_file (str): Der Pfad zur CSV-Datei.
        data_path (str): Der Zielordner, in den die Repos geklont werden sollen.
    """
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    with open(csv_file, mode='r', encoding="utf-8-sig") as file:
        reader = csv.reader(file, delimiter=';')
        for idx, row in enumerate(reader):
            repo_url = row[2]
            if not repo_url:
                error_message = f'Keine Repo-URL in Zeile {idx+1} gefunden: {row[0]}'
                with open('error_log.txt', 'a') as error_file:
                    error_file.write(error_message + '\n')
                print(error_message)
                continue
            
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            repo_path = os.path.join(data_path, repo_name)
            if os.path.exists(repo_path):
                print(f'Repo {repo_name} existiert bereits, überspringe Klonen.')
                continue
            
            try:
                subprocess.run(['git', 'clone', repo_url], cwd=data_path, check=True)
                print(f'Klonen von {repo_url} erfolgreich.')
            except subprocess.CalledProcessError as e:
                error_message = f'Fehler beim Klonen von {repo_url} in Zeile {idx+1}, {row[0]}: {e}'
                with open('error_log.txt', 'a') as error_file:
                    error_file.write(error_message + '\n')
                print(error_message)




if __name__ == "__main__":
    csv_file = "/Users/david/Development/fenexity/data/repos.csv"
    data_path = "/Users/david/Development/fenexity/data/graph_repos"
    clone_repos_from_csv(csv_file, data_path)
