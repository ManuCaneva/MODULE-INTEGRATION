import { SetMetadata } from '@nestjs/common';

export const ROLES_KEY = 'roles';
// Accepts one or more role names
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);