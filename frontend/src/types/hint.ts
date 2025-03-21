export interface HintResponse {
    hint: string;
    solver_type: string;
    candidates_remaining: number;
}

export interface SolverInfo {
    id: string;
    name: string;
    description: string;
} 