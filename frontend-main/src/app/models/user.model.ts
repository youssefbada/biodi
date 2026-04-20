export interface User {
  id: number;
  nni: string;
  role: 'ADMIN' | 'READONLY';
  is_active: boolean;
  sub: string;
  uid: string;
  name: string;
  givenName: string;
  sn: string;
  mail: string | null;
}

export interface AuthResponse {
  authenticated: boolean;
  authorized?: boolean;
  reason?: string;
  code?: string;
  detail?: string;
  user?: User;
}
