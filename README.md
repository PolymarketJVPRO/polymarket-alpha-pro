# Polymarket Alpha Pro

Dashboard operable para escanear mercados de Polymarket, calcular score y generar señales: BUY YES / BUY NO / NO TRADE.

## Uso local en Windows

1. Instala Python desde https://www.python.org/downloads/ y marca **Add Python to PATH**.
2. Abre la carpeta del proyecto.
3. Ejecuta `install_windows.bat`.
4. Ejecuta `run_windows.bat`.

## Despliegue en Render

1. Sube todos estos archivos al repositorio de GitHub.
2. En Render: New > Web Service.
3. Conecta el repositorio.
4. Usa estos comandos:

Build command:
```bash
pip install -r requirements.txt
```

Start command:
```bash
streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0
```

## Qué hace v1

- Descubre mercados activos de Polymarket.
- Filtra por volumen y liquidez.
- Calcula score 0-100.
- Clasifica BUY YES / BUY NO / NO TRADE.
- Exporta CSV.
- Incluye watchlist manual.

## Nota importante

Esto no es asesoría financiera. El score ayuda a filtrar oportunidades, pero ninguna señal garantiza ganancias.
