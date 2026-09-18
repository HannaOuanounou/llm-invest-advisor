import { Box, Paper, Typography } from "@mui/material";
import { Light as SyntaxHighlighter } from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

const AnalysisResult = ({ analysisMessage }: { analysisMessage: string }) => {
  return (
    <Box sx={{ mt: 2 }}>
      {  (
        analysisMessage && (
          <Paper sx={{ p: 2, borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>
              Analyse 10-K :
            </Typography>
            <SyntaxHighlighter language="json" style={docco}>
              {analysisMessage}
            </SyntaxHighlighter>
          </Paper>
        )
      )}
    </Box>
  );
};

export default AnalysisResult;
