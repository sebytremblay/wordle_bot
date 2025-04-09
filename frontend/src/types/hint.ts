export interface HintResponse {
    hint: string;
    solver_type: string;
    cached: boolean;
    game_id: string;
}

export interface SolverInfo {
    id: string;
    name: string;
    description: string;
}