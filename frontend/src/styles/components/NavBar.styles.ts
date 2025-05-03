import styled from '@emotion/styled';
import { Link } from 'react-router-dom';
import { theme } from '../theme';
import isPropValid from '@emotion/is-prop-valid';

const customShouldForwardProp = (prop: string) => isPropValid(prop) && prop !== '$active';

export const NavContainer = styled.nav`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: ${theme.colors.background.primary};
    box-shadow: ${theme.shadows.sm};
    z-index: 1000;
    padding: ${theme.spacing.xs} ${theme.spacing.sm};
`;

export const NavContent = styled.div`
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    justify-content: space-around;
    align-items: center;
`;

export const NavLink = styled(Link, { shouldForwardProp: customShouldForwardProp }) <{ $active: boolean }>`
    color: ${props => props.$active ? theme.colors.primary : theme.colors.text.primary};
    text-decoration: none;
    font-weight: ${props => props.$active ? 'bold' : 'normal'};
    padding: ${theme.spacing.xs} ${theme.spacing.sm};
    border-bottom: 2px solid ${props => props.$active ? theme.colors.primary : 'transparent'};
    transition: all 0.2s ease-in-out;

    &:hover {
        color: ${theme.colors.primary};
        border-bottom-color: ${theme.colors.primary};
    }
`; 