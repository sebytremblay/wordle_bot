import React, { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import { getSolvers } from '../services/api';
import { SolverInfo } from '../types/solvers';

const Container = styled.div`
    max-width: 800px;
    margin: 60px auto 0;
    padding: 2rem 1rem;
`;

const Title = styled.h1`
    text-align: center;
    color: #1a1a1b;
    margin-bottom: 2rem;
`;

const SolverGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding: 1rem;
`;

const SolverCard = styled.div`
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease-in-out;

    &:hover {
        transform: translateY(-4px);
    }
`;

const SolverName = styled.h2`
    color: #1a1a1b;
    margin-bottom: 1rem;
    font-size: 1.5rem;
`;

const SolverDescription = styled.p`
    color: #787c7e;
    line-height: 1.5;
`;

const AboutPage: React.FC = () => {
    const [solvers, setSolvers] = useState<SolverInfo[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchSolvers = async () => {
            try {
                const response = await getSolvers();
                setSolvers(response.solvers);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to fetch solvers');
            }
        };

        fetchSolvers();
    }, []);

    if (error) {
        return (
            <Container>
                <Title>Error</Title>
                <p style={{ textAlign: 'center', color: 'red' }}>{error}</p>
            </Container>
        );
    }

    return (
        <Container>
            <Title>About the Solvers</Title>
            <SolverGrid>
                {solvers.map((solver) => (
                    <SolverCard key={solver.id}>
                        <SolverName>{solver.name}</SolverName>
                        <SolverDescription>{solver.description}</SolverDescription>
                    </SolverCard>
                ))}
            </SolverGrid>
        </Container>
    );
};

export default AboutPage; 