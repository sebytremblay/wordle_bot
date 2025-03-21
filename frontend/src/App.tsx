import React from 'react';
import { ThemeProvider } from 'styled-components';
import { theme } from './theme';
import HomePage from './pages/HomePage';
import ErrorBoundary from './components/ErrorBoundary';
import { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
    body {
        margin: 0;
        font-family: 'Clear Sans', 'Helvetica Neue', Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    * {
        box-sizing: border-box;
    }
`;

const App = () => {
    return (
        <ThemeProvider theme={theme}>
            <GlobalStyles />
            <ErrorBoundary>
                <HomePage />
            </ErrorBoundary>
        </ThemeProvider>
    );
};

export default App; 