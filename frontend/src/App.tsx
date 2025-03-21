import React from 'react';
import { Global, css } from '@emotion/react';
import HomePage from './pages/HomePage';

const globalStyles = css`
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    },
    'html, body': {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #ffffff;
        color: #1a1a1b;
    },
    'button, input, select': {
        font-family: inherit;
    },
`;

const App: React.FC = () => (
    <>
        <Global styles={globalStyles} />
        <HomePage />
    </>
);

export default App; 