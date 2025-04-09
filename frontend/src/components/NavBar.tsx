import React from 'react';
import { useLocation } from 'react-router-dom';
import { NavContainer, NavContent, NavLink } from '../styles/components/NavBar.styles';

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