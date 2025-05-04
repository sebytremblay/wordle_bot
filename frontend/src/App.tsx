import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from '@emotion/styled';
import NavBar from './components/NavBar';
import HomePage from './pages/HomePage';
import PlayAgainstSolverPage from './pages/PlayAgainstSolverPage';
import AboutPage from './pages/AboutPage';
import ResultsPage from './pages/ResultsPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const AppContainer = styled.div`
    min-height: 100vh;
    background-color: #f9f9f9;
`;

const App: React.FC = () => {
    return (
        <Router>
            <AppContainer>
                <NavBar />
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/play-against-solver" element={<PlayAgainstSolverPage />} />
                    <Route path="/about" element={<AboutPage />} />
                    <Route path="/results" element={<ResultsPage />} />
                </Routes>
                <ToastContainer
                    position="top-center"
                    autoClose={10000}
                    hideProgressBar={false}
                    newestOnTop={false}
                    closeOnClick
                    rtl={false}
                    pauseOnFocusLoss
                    draggable
                    theme="colored"
                />
            </AppContainer>
        </Router>
    );
};

export default App; 