import { ReactNode } from 'react';
import SideMenu from '../components/admin/side_menu';

interface LayoutProps {
  children: ReactNode;
}

export default function SuperAdmin({ children }: LayoutProps) {
  return (
    <div className="flex">
      <SideMenu />
      <div className="flex-1 sm:ml-64 p-4">
        {children}
      </div>
    </div>

  );
}
