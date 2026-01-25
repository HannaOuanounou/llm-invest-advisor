import { useState } from "react";
import { api } from "./api/backend";
import { Box, Button, TextField, CircularProgress, Container } from "@mui/material";
import AnalysisResult from "../component/AnalysisResult";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import SearchBar from "../component/SearchBar";

const theme = createTheme({
  palette: {
    primary: {
      main: "#03192fff", 
    },
    secondary: {
      main: "#f50057", 
    },
    background: {
      default: "#f4f6f8", 
      paper: "#ffffff",   
    },
    text: {
      primary: "#212121", // Texte sombre pour la lisibilité
    },
  },
});

function App() {
  const [ticker, setTicker] = useState<string>("");
  const [analysisMessage, setAnalysisMessage] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  // Handle backend analysis request
  const handleAnalyze = async () => {
    if (!ticker) return; // Don't run if no ticker
    setLoading(true);
    setAnalysisMessage(""); // Reset previous analysis message

    try {
      const response = await api.get("/10K_Analysis/", {
        params: { ticker },
      });
      setAnalysisMessage(JSON.stringify(response.data.summaries, null, 2)); 
    } catch (error) {
      console.error(error);
      setAnalysisMessage("Error occurred during analysis");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      {/* Application avec fond clair */}
      <Container
        sx={{
          backgroundColor: theme.palette.background.default,
          minHeight: "100vh", // S'assurer que la page occupe toute la hauteur de l'écran
          display: "flex",
          flexDirection: "column",
          justifyContent: "center", // Centrer verticalement
          p: 2,
        }}
      >
        {/* SearchBar */}
        <SearchBar />

        {/* Formulaire de recherche */}
        <Box sx={{ mb: 2 }}>
          <TextField
            label="Ticker"
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            fullWidth
            variant="outlined"
            sx={{ mb: 2 }} 
          />
          <Button
            variant="contained"
            onClick={handleAnalyze}
            disabled={loading}
            fullWidth
            sx={{
              backgroundColor: theme.palette.primary.main,
              '&:hover': {
                backgroundColor: theme.palette.primary.dark, 
              },
            }}
          >
            {loading ? <CircularProgress size={24} /> : "Analyser 10-K"}
          </Button>
        </Box>

        <AnalysisResult analysisMessage={analysisMessage} />
      </Container>
    </ThemeProvider>
  );
}

export default App;
