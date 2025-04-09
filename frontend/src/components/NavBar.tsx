import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from '@emotion/styled';

const NavContainer = styled.nav`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #ffffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    padding: 0.5rem 1rem;
`;

const NavContent = styled.div`
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    justify-content: space-around;
    align-items: center;
`;

const NavLink = styled(Link) <{ $active: boolean }>`
    color: ${props => props.$active ? '#6aaa64' : '#1a1a1b'};
    text-decoration: none;
    font-weight: ${props => props.$active ? 'bold' : 'normal'};
    padding: 0.5rem 1rem;
    border-bottom: 2px solid ${props => props.$active ? '#6aaa64' : 'transparent'};
    transition: all 0.2s ease-in-out;

    &:hover {
        color: #6aaa64;
        border-bottom-color: #6aaa64;
    }
`;

const NavBar: React.FC = () => {
    const location = useLocation();

    return (
        <NavContainer>
            <NavContent>
                <NavLink to="/" $active={location.pathname === '/'}>
                    Home
                </NavLink>
                <NavLink to="/play-against-solver" $active={location.pathname === '/play-against-solver'}>
                    Play Against a Solver
                </NavLink>
                <NavLink to="/about" $active={location.pathname === '/about'}>
                    About the Solvers
                </NavLink>
            </NavContent>
        </NavContainer>
    );
};

export default NavBar; 