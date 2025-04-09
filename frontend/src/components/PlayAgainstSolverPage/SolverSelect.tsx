import React, { useState, useEffect } from 'react';
import styled from '@emotion/styled';
import { SolverInfo } from '@/types/hint';
import { getSolvers } from '@/services/api';

interface SolverSelectProps {
    disabled?: boolean;
    onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}

const Panel = styled.div`
  width: 50%;
  margin: 0px 15px;
  padding: 15px;
  border: 2px solid #d3d6da;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
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

const ErrorMessage = styled.div`
  color: red;
  margin-top: 10px;
  text-align: center;
`;

const SolverSelect: React.FC<SolverSelectProps> = ({ disabled, onChange }) => {
    const [solvers, setSolvers] = useState<SolverInfo[]>([]);
    const [selectedSolver, setSelectedSolver] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchSolvers = async () => {
            try {
                setLoading(true);

                const response = await getSolvers();
                setSolvers(response.solvers);
                setSelectedSolver(response.solvers[0]?.id || '');
            } catch (err) {
                setError('Failed to load solvers');
            } finally {
                setLoading(false);
            }
        };

        fetchSolvers();
    }, []);


    return (
        <Panel>
            <Select
                value={selectedSolver}
                onChange={(e) => {
                    setSelectedSolver(e.target.value);
                    onChange(e);
                }}
                disabled={disabled || loading}
            >
                <option value="">Select a solver</option>
                {solvers.map((solver) => (
                    <option key={solver.id} value={solver.id}>
                        {solver.name}
                    </option>
                ))}
            </Select>

            {error && <ErrorMessage>{error}</ErrorMessage>}
        </Panel>
    );
};

export default SolverSelect; 