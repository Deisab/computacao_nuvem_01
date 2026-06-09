from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI(title="ERP Restaurante - Gestão de Insumos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.48.62"),
    "database": os.getenv("DB_NAME", "restaurante"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "gabriel10")
}

class Insumo(BaseModel):
    produto: str
    qtd: int

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

@app.on_event("startup")
def criar_tabela():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                id SERIAL PRIMARY KEY,
                produto VARCHAR(100) NOT NULL,
                qtd INTEGER NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[ERRO startup]: {e}")

@app.get("/")
def home():
    return {"status": "Online", "projeto": "ERP Gastronomia"}

@app.get("/estoque")
def listar():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, produto, qtd FROM estoque ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": r[0], "produto": r[1], "quantidade": r[2]} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/estoque")
def adicionar(insumo: Insumo):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO estoque (produto, qtd) VALUES (%s, %s) RETURNING id;", (insumo.produto, insumo.qtd))
        novo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"id": novo_id, "produto": insumo.produto, "quantidade": insumo.qtd}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/estoque/{id}")
def atualizar(id: int, insumo: Insumo):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE estoque SET produto=%s, qtd=%s WHERE id=%s;", (insumo.produto, insumo.qtd, id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Insumo não encontrado")
        conn.commit()
        cur.close()
        conn.close()
        return {"id": id, "produto": insumo.produto, "quantidade": insumo.qtd}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/estoque/{id}")
def deletar(id: int):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM estoque WHERE id=%s;", (id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Insumo não encontrado")
        conn.commit()
        cur.close()
        conn.close()
        return {"mensagem": f"Insumo {id} removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
