const express = require("express");
const fetch = require("node-fetch");
const cors = require("cors");

const app = express();
app.use(cors());

const PORT = process.env.PORT || 3000;
const BCH_API_KEY = "57a1e73f68904bbdb91101a070bc822c";
const BCH_URL = "https://bchapi-am.developer.azure-api.net/api/v1/indicadores/620/cifras";

app.get("/tipocambio", async (req, res) => {
  try {
    const response = await fetch(BCH_URL, {
      headers: {
        "Ocp-Apim-Subscription-Key": BCH_API_KEY,
      },
    });

    const data = await response.json();
    const valorVenta = data[0]?.Valor;

    if (valorVenta) {
      res.json({ tipoCambio: valorVenta });
    } else {
      res.status(500).json({ error: "Valor no encontrado" });
    }
  } catch (error) {
    res.status(500).json({ error: "Error al conectar con la API del BCH" });
  }
});

app.listen(PORT, () => {
  console.log(`Servidor funcionando en puerto ${PORT}`);
});
