import styled from '@emotion/styled';

export const ViewerContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 700px;
`;

export const Controls = styled.div`
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
`;

export const StyledPage = styled.div<{ width: number }>`
  box-shadow: 0 2px 8px rgba(0,0,0,0.10);
  margin-bottom: 1rem;
  background: #f9f9f9;
  border-radius: 4px;
  overflow: hidden;
  width: ${({ width }) => width}px;
  max-width: 100%;
`;

export const PageInfo = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 0.25rem;
  padding-bottom: 2rem;
  color: #787c7e;
`; 