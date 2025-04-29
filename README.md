# 📍 Geolocalização de Postos de Combustíveis e Usinas

Este projeto utiliza Python, Dash e Folium para criar um painel interativo que combina visualizações estatísticas com geolocalização dos postos de combustíveis e das usinas produtoras. A ferramenta facilita a análise territorial da tancagem, presença de produtos e proximidade com usinas, oferecendo insights úteis para planejamento logístico, análise de mercado e políticas públicas.

## 🔍 Funcionalidades

- 📊 Gráficos interativos com número de postos por produto e tancagem total.
- 🗺️ Mapa com geolocalização dos postos por produto (com camadas ativáveis).
- 🏭 Localização das usinas com raio de influência de 20 km.
- 📂 Dados lidos a partir de planilhas Excel.
- 📌 Conversão automática de coordenadas DMS para decimal.
- 💾 Exportação do mapa em HTML.


## ▶️ Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Marcelo0010/Geolocaliza-o-POstos.git
   cd Geolocaliza-o-POstos

2. Instale as dependências:

pip install -r requirements.txt

3. Edite o caminho do arquivo Excel no script principal:

file_path = r"D:ADICIONE AQUI O CAMINHO DO ARQUIVO"

4. Execute o painel:

python mapa_postos_modelo.py

