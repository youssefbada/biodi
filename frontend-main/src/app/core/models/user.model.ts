export interface OidcUser {
  sub?: string;
  name?: string;
  mail?: string;
  [key: string]: any;
}

export interface MeResponse {
  authenticated: boolean;
  user?: OidcUser;
}
