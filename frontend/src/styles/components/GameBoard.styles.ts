import styled from '@emotion/styled';
import { theme } from '../theme';

interface CellProps {
    status?: 'correct' | 'present' | 'absent';
}

export const Grid = styled.div`
    display: grid;
    grid-template-rows: repeat(6, 1fr);
    gap: 5px;
    padding: ${theme.spacing.sm};
    width: 350px;
    margin: 0 auto;
    
    @media (min-width: ${theme.breakpoints.mobile}) {
        width: 390px;
    }
`;

export const Row = styled.div`
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 5px;
`;

export const Cell = styled.div<CellProps>`
    width: 100%;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    aspect-ratio: 1;
    font-size: ${theme.typography.fontSizes.xlarge};
    font-weight: bold;
    vertical-align: middle;
    box-sizing: border-box;
    color: ${(props: CellProps) => props.status ? theme.colors.background.primary : theme.colors.text.primary};
    text-transform: uppercase;
    user-select: none;
    
    border: 2px solid ${(props: CellProps) => props.status ? 'transparent' : theme.colors.border};
    background-color: ${(props: CellProps) => {
        switch (props.status) {
            case 'correct':
                return theme.colors.cell.correct;
            case 'present':
                return theme.colors.cell.present;
            case 'absent':
                return theme.colors.cell.absent;
            default:
                return theme.colors.background.primary;
        }
    }};
    
    transform-style: preserve-3d;
    transition: transform 0.6s;
    transform: ${(props: CellProps) => props.status ? 'rotateX(360deg)' : 'none'};
    
    @media (min-width: ${theme.breakpoints.mobile}) {
        font-size: 2.25rem;
    }
`; 