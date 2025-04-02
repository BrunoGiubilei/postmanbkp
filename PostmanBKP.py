import requests
from dotenv import load_dotenv
import os
import subprocess
import time

load_dotenv()

# Configurações
POSTMAN_API_KEY = os.getenv("POSTMAN_API_KEY")
REPO_PATH = "C:\Projetos\GitHub\postmanbkp"
POSTMAN_WORKSPACE_ID = "SEU_WORKSPACE_ID"  # Opcional se quiser gerenciar por workspace
CHECK_INTERVAL = 30  # Intervalo para verificar alterações (em segundos)

# Cabeçalhos para a API do Postman
HEADERS = {
    "X-Api-Key": POSTMAN_API_KEY,
    "Content-Type": "application/json"
}

def export_collections():
    """Exporta todas as coleções do Postman e salva no repositório local."""
    url = "https://api.getpostman.com/collections"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        collections = response.json()["collections"]
        for collection in collections:
            collection_id = collection["uid"]
            collection_name = collection["name"]
            export_url = f"https://api.getpostman.com/collections/{collection_id}"
            export_response = requests.get(export_url, headers=HEADERS)

            if export_response.status_code == 200:
                file_path = os.path.join(REPO_PATH, f"{collection_name}.json")
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(export_response.text)
                print(f"Coleção '{collection_name}' exportada com sucesso.")
            else:
                print(f"Falha ao exportar a coleção '{collection_name}'.")
    else:
        print("Erro ao obter coleções:", response.status_code)

def sync_repository():
    """Sincroniza o repositório local com o repositório remoto."""
    try:
        subprocess.run(["git", "-C", REPO_PATH, "add", "."], check=True)
        subprocess.run(["git", "-C", REPO_PATH, "commit", "-m", "Atualizando coleções do Postman"], check=True)
        subprocess.run(["git", "-C", REPO_PATH, "push"], check=True)
        print("Repositório sincronizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao sincronizar repositório: {e}")

def pull_and_import():
    """Atualiza o repositório local e importa as alterações para o Postman."""
    try:
        subprocess.run(["git", "-C", REPO_PATH, "pull"], check=True)
        for file_name in os.listdir(REPO_PATH):
            if file_name.endswith(".json"):
                file_path = os.path.join(REPO_PATH, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    data = file.read()
                # Aqui você poderia implementar lógica para importar automaticamente para o Postman, caso necessário.
                print(f"Arquivo '{file_name}' pronto para importação.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar repositório: {e}")

def main():
    """Execução principal."""
    while True:
        print("Exportando coleções do Postman...")
        export_collections()
        print("Sincronizando com o repositório...")
        sync_repository()
        print("Verificando novas alterações no repositório...")
        pull_and_import()
        print(f"Aguardando {CHECK_INTERVAL} segundos até a próxima verificação...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
