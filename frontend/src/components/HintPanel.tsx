import React, { useState, useEffect } from 'react';
import styled from '@emotion/styled';
import { SolverInfo } from '../types/hint';
import { getHint, getSolvers } from '../services/api';

interface HintPanelProps {
    gameId: string;
    disabled?: boolean;
}

const Panel = styled.div`
  max-width: 350px;
  margin: 20px auto;
  padding: 15px;
  border: 2px solid #d3d6da;
  border-radius: 4px;
`;

const Select = styled.select`
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  font-size: 1rem;
  border: 1px solid #d3d6da;
  border-radius: 4px;
  &:disabled {
    background-color: #f0f0f0;
    cursor: not-allowed;
  }
`;

const Button = styled.button`
  width: 100%;
  padding: 10px;
  font-size: 1.2rem;
  background-color: #538d4e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  &:hover:not(:disabled) {
    background-color: #3a6b37;
  }
`;

const HintDisplay = styled.div`
  margin-top: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-size: 1.1rem;
  text-align: center;
`;

const ErrorMessage = styled.div`
  color: red;
  margin-top: 10px;
  text-align: center;
`;

const HintPanel: React.FC<HintPanelProps> = ({ gameId, disabled }) => {
    const [solvers, setSolvers] = useState<SolverInfo[]>([]);
    const [selectedSolver, setSelectedSolver] = useState('');
    const [hint, setHint] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchSolvers = async () => {
            try {
                const response = await getSolvers();
                setSolvers(response.solvers);
                setSelectedSolver(response.solvers[0]?.id || '');
            } catch (err) {
                setError('Failed to load solvers');
            }
        };

        fetchSolvers();
    }, []);

    const requestHint = async () => {
        if (!selectedSolver) return;

        setLoading(true);
        setError(null);
        try {
            const response = await getHint(gameId, selectedSolver);
            setHint(response.hint);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to get hint');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Panel>
            <Select
                value={selectedSolver}
                onChange={(e) => setSelectedSolver(e.target.value)}
                disabled={disabled || loading}
            >
                <option value="">Select a solver</option>
                {solvers.map((solver) => (
                    <option key={solver.id} value={solver.id}>
                        {solver.name}
                    </option>
                ))}
            </Select>

            <Button
                onClick={requestHint}
                disabled={disabled || loading || !selectedSolver}
            >
                {loading ? 'Getting hint...' : 'Get Hint'}
            </Button>

            {hint && (
                <HintDisplay>
                    Suggested word: <strong>{hint.toUpperCase()}</strong>
                </HintDisplay>
            )}

            {error && <ErrorMessage>{error}</ErrorMessage>}
        </Panel>
    );
};

export default HintPanel; 