'use client';

import { Outlet, Link } from "react-router-dom";
import { useCurrentUserStore } from "../../utils/hooks/use_current_user";
import HandleLogout from "../viewModel/handle_logout";

export default function NavbarLayout() {
  const { user } = useCurrentUserStore();



  return (
    <>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg bg-white shadow-sm border-bottom">
        <div className="container-fluid">
          {/* Brand */}
          <Link className="navbar-brand fw-bold text-primary" to="/">
            GENE-XX
          </Link>

          {/* Mobile Toggle Button */}
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarContent"
            aria-controls="navbarContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          {/* Collapsible Menu */}
          <div className="collapse navbar-collapse" id="navbarContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <Link className="nav-link text-dark" to="/dashboard">
                  Dashboard
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link text-dark" to="/profile">
                  Profile
                </Link>
              </li>
            </ul>

            {/* Right Side: User + Logout */}
            <div className="d-flex align-items-center gap-3">
              {user && (
                <span className="text-dark small bg-light px-3 py-1 rounded-pill border">
                  {user.fullName}
                </span>
              )}
              <button
                onClick={HandleLogout}
                className="btn btn-outline-danger btn-sm"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <main className="flex-grow-1 p-4 bg-light h-100 default-page">
        <Outlet />
      </main>
    </>
  );
}