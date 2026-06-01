from fastapi import FastAPI
import psycopg2

app = FastAPI(title="ERP Restaurante - Logística")

DB_CONFIG = {
	"host": "192.168.48.62",
	"database": "restaurante",
	"user": "admin",
	"password": "gabriel10"
}

def get_estoque_db():
	try:
		conn = psycopg2.connect(**DB_CONFIG)
		cur = conn.cursor()
		cur.execute("SELECT id, produto, qtd FROM estoque;")
		rows = cur.fetchall()
		cur.close()
		conn.close()
		return rows
	except Exception as e:
		print(f"\n[ERRO CRÍTICO DB]: {e}\n")
		return f"Erro de conexão: {e}"

@app.get("/")
def home():
	return {"status":"Online","projeto": "TCC ERP Gastronomia"}

@app.get("/estoque")
def listar_estoque():
	dados = get_estoque_db()
	if isinstance(dados, str):
		return {"erro": dados}

	lista_estoque = [
		{"id": r[0], "produto": r[1], "quantidade": r[2]}
		for r in dados
	]
	return lista_estoque
