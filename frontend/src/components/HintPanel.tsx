import React, { useState } from 'react';
import styled from 'styled-components';
import { getHint, getSolvers } from '../services/api';
import { SolverInfo } from '../types/hint';
import { HintPanelProps } from 'types/components';
import { logger } from '../utils/logger';

const Panel = styled.div`
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 8px;
    margin-top: 20px;
`;

const Title = styled.h3`
    margin: 0 0 15px 0;
    color: #333;
`;

const HintButton = styled.button`
    width: 100%;
    padding: 10px 20px;
    font-size: 1.2rem;
    background-color: ${props => props.theme.colors.secondary};
    color: ${props => props.theme.colors.white};
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 10px;

    &:hover:not(:disabled) {
        filter: brightness(0.9);
    }

    &:disabled {
        background-color: ${props => props.theme.colors.gray};
        cursor: not-allowed;
    }
`;

const HintText = styled.div`
    text-align: center;
    margin: 10px 0;
    padding: 10px;
    background-color: ${props => props.theme.colors.border};
    border-radius: 4px;
    font-size: 1.2rem;
`;

const ErrorText = styled.div`
    color: ${props => props.theme.colors.error};
    text-align: center;
    margin-top: 10px;
    font-size: 1rem;
`;

const SolverSelect = styled.select`
    width: 100%;
    padding: 10px;
    font-size: 1.2rem;
    border: 2px solid ${props => props.theme.colors.border};
    border-radius: 4px;
    margin-bottom: 10px;
    cursor: pointer;

    &:disabled {
        background-color: ${props => props.theme.colors.gray};
        cursor: not-allowed;
    }

    &:focus {
        outline: none;
        border-color: ${props => props.theme.colors.secondary};
    }
`;

const HintPanel: React.FC<HintPanelProps> = ({ gameId, disabled }) => {
    const [hint, setHint] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [solvers, setSolvers] = useState<SolverInfo[]>([]);
    const [selectedSolver, setSelectedSolver] = useState('');

    React.useEffect(() => {
        const loadSolvers = async () => {
            try {
                const response = await getSolvers();
                setSolvers(response.solvers);
                if (response.solvers.length > 0) {
                    setSelectedSolver(response.solvers[0].id);
                }
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : 'Failed to load solvers';
                setError(errorMessage);
                logger.error('HintPanel', 'Error loading solvers:', err);
            }
        };

        loadSolvers();
    }, []);

    const handleGetHint = async () => {
        setIsLoading(true);
        setError('');

        try {
            const response = await getHint(gameId, selectedSolver);
            setHint(response.hint);
            logger.debug('HintPanel', 'Hint received:', response);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to get hint';
            setError(errorMessage);
            logger.error('HintPanel', 'Error getting hint:', err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Panel>
            <Title>Hint Panel</Title>
            <SolverSelect
                value={selectedSolver}
                onChange={(e) => setSelectedSolver(e.target.value)}
                disabled={disabled || isLoading}
            >
                {solvers.map(solver => (
                    <option key={solver.id} value={solver.id}>
                        {solver.name}
                    </option>
                ))}
            </SolverSelect>
            <HintButton
                onClick={handleGetHint}
                disabled={disabled || isLoading || !selectedSolver}
            >
                {isLoading ? 'Getting Hint...' : 'Get Hint'}
            </HintButton>
            {hint && <HintText>Suggested word: {hint}</HintText>}
            {error && <ErrorText>{error}</ErrorText>}
        </Panel>
    );
};

export default HintPanel; 