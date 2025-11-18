
"use client";
import Link from "next/link";
import React, { useState } from "react";
import { Box, ChevronLeft, ChevronRight, Package, ShoppingCart } from "lucide-react";

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div
      className={`h-screen bg-gray-800 text-white transition-all duration-300 ${
        isCollapsed ? "w-20" : "w-64"
      }`}
    >
      <div className="flex items-center justify-between p-4">
        {!isCollapsed && (
          <h1 className="text-2xl font-bold">Stock System</h1>
        )}
        <button onClick={toggleSidebar} className="p-2">
          {isCollapsed ? <ChevronRight /> : <ChevronLeft />}
        </button>
      </div>
      <nav>
        <ul>
          <li className="p-4 hover:bg-gray-700">
            <Link href="/products" className="flex items-center">
              <Package className="mr-2" />
              {!isCollapsed && "Productos"}
            </Link>
          </li>
          <li className="p-4 hover:bg-gray-700">
            <Link href="/categories" className="flex items-center">
              <Box className="mr-2" />
              {!isCollapsed && "Categorías"}
            </Link>
          </li>
          <li className="p-4 hover:bg-gray-700">
            <Link href="/reservations" className="flex items-center">
              <ShoppingCart className="mr-2" />
              {!isCollapsed && "Reservas"}
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
