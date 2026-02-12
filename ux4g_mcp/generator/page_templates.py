"""Page-level templates for common UX4G patterns."""
from typing import Dict, Optional


class PageTemplates:
    """Templates for full page structures using UX4G components and utilities."""

    @staticmethod
    def landing_page(title: str = "Department Portal", dept_name: str = "Department", framework: str = "html") -> str:
        """Generate a complete landing page using ONLY UX4G utility classes - NO custom CSS."""
        class_attr = "className" if framework == "react" else "class"
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Government Portal</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/css/ux4g.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/css/ux4g-grid.css">
</head>
<body class="bg-light">
    <!-- Navigation -->
    <nav {class_attr}="navbar navbar-expand-lg bg-white shadow-sm border-bottom border-success border-3">
        <div {class_attr}="container">
            <a {class_attr}="navbar-brand fw-bold text-success text-decoration-none" href="#">{dept_name}</a>
            <button {class_attr}="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span {class_attr}="navbar-toggler-icon"></span>
            </button>
            <div {class_attr}="collapse navbar-collapse" id="navbarNav">
                <ul {class_attr}="navbar-nav ms-auto">
                    <li {class_attr}="nav-item">
                        <a {class_attr}="nav-link active" href="#home">Home</a>
                    </li>
                    <li {class_attr}="nav-item">
                        <a {class_attr}="nav-link" href="#programs">Programs</a>
                    </li>
                    <li {class_attr}="nav-item">
                        <a {class_attr}="nav-link" href="#services">Services</a>
                    </li>
                    <li {class_attr}="nav-item">
                        <a {class_attr}="nav-link" href="#contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section {class_attr}="bg-success bg-gradient text-white py-5" id="home">
        <div {class_attr}="container">
            <div {class_attr}="row align-items-center">
                <div {class_attr}="col-lg-8">
                    <h1 {class_attr}="display-4 fw-bold mb-4">Empowering Communities</h1>
                    <p {class_attr}="lead mb-4">Building sustainable futures through innovative programs and community engagement.</p>
                    <div {class_attr}="d-flex gap-3">
                        <button type="button" {class_attr}="btn btn-light btn-lg">Explore Programs</button>
                        <button type="button" {class_attr}="btn btn-outline-light btn-lg">Apply for Benefits</button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section {class_attr}="py-5 bg-white">
        <div {class_attr}="container">
            <div {class_attr}="row g-4">
                <div {class_attr}="col-md-3 col-sm-6">
                    <div {class_attr}="text-center">
                        <div {class_attr}="display-4 fw-bold text-success mb-2">2.5M+</div>
                        <p {class_attr}="text-muted mb-0">Beneficiaries Reached</p>
                    </div>
                </div>
                <div {class_attr}="col-md-3 col-sm-6">
                    <div {class_attr}="text-center">
                        <div {class_attr}="display-4 fw-bold text-success mb-2">15K+</div>
                        <p {class_attr}="text-muted mb-0">Villages Connected</p>
                    </div>
                </div>
                <div {class_attr}="col-md-3 col-sm-6">
                    <div {class_attr}="text-center">
                        <div {class_attr}="display-4 fw-bold text-success mb-2">₹500Cr</div>
                        <p {class_attr}="text-muted mb-0">Funds Disbursed</p>
                    </div>
                </div>
                <div {class_attr}="col-md-3 col-sm-6">
                    <div {class_attr}="text-center">
                        <div {class_attr}="display-4 fw-bold text-success mb-2">125+</div>
                        <p {class_attr}="text-muted mb-0">Active Programs</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Programs Section -->
    <section {class_attr}="py-5" id="programs">
        <div {class_attr}="container">
            <div {class_attr}="text-center mb-5">
                <h2 {class_attr}="display-5 fw-bold mb-3">Key Programs & Initiatives</h2>
                <p {class_attr}="lead text-muted">Comprehensive schemes designed to transform communities</p>
            </div>
            <div {class_attr}="row g-4">
                <div {class_attr}="col-md-4">
                    <div {class_attr}="card h-100 shadow-sm">
                        <div {class_attr}="card-body">
                            <span {class_attr}="badge bg-success mb-3">ACTIVE</span>
                            <h5 {class_attr}="card-title">Program Name</h5>
                            <p {class_attr}="card-text">Program description and benefits for beneficiaries.</p>
                            <button type="button" {class_attr}="btn btn-primary">Learn More</button>
                        </div>
                    </div>
                </div>
                <div {class_attr}="col-md-4">
                    <div {class_attr}="card h-100 shadow-sm">
                        <div {class_attr}="card-body">
                            <span {class_attr}="badge bg-success mb-3">ACTIVE</span>
                            <h5 {class_attr}="card-title">Program Name</h5>
                            <p {class_attr}="card-text">Program description and benefits for beneficiaries.</p>
                            <button type="button" {class_attr}="btn btn-primary">Learn More</button>
                        </div>
                    </div>
                </div>
                <div {class_attr}="col-md-4">
                    <div {class_attr}="card h-100 shadow-sm">
                        <div {class_attr}="card-body">
                            <span {class_attr}="badge bg-success mb-3">ACTIVE</span>
                            <h5 {class_attr}="card-title">Program Name</h5>
                            <p {class_attr}="card-text">Program description and benefits for beneficiaries.</p>
                            <button type="button" {class_attr}="btn btn-primary">Learn More</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section {class_attr}="py-5 bg-light" id="services">
        <div {class_attr}="container">
            <div {class_attr}="text-center mb-5">
                <h2 {class_attr}="display-5 fw-bold mb-3">Online Services</h2>
                <p {class_attr}="lead text-muted">Quick access to essential services</p>
            </div>
            <div {class_attr}="row g-4">
                <div {class_attr}="col-md-3 col-sm-6">
                    <div {class_attr}="card text-center h-100">
                        <div {class_attr}="card-body">
                            <div {class_attr}="fs-1 mb-3">📝</div>
                            <h5 {class_attr}="card-title">Apply for Benefits</h5>
                            <p {class_attr}="card-text text-muted">Submit applications online</p>
                        </div>
                    </div>
                </div>
                <div {class_attr}="col-md-3 col-sm-6">
                    <div {class_attr}="card text-center h-100">
                        <div {class_attr}="card-body">
                            <div {class_attr}="fs-1 mb-3">🔍</div>
                            <h5 {class_attr}="card-title">Track Application</h5>
                            <p {class_attr}="card-text text-muted">Check application status</p>
                        </div>
                    </div>
                </div>
                <div {class_attr}="col-md-3 col-sm-6">
                    <div {class_attr}="card text-center h-100">
                        <div {class_attr}="card-body">
                            <div {class_attr}="fs-1 mb-3">📄</div>
                            <h5 {class_attr}="card-title">Download Forms</h5>
                            <p {class_attr}="card-text text-muted">Access application forms</p>
                        </div>
                    </div>
                </div>
                <div {class_attr}="col-md-3 col-sm-6">
                    <div {class_attr}="card text-center h-100">
                        <div {class_attr}="card-body">
                            <div {class_attr}="fs-1 mb-3">📞</div>
                            <h5 {class_attr}="card-title">Helpline</h5>
                            <p {class_attr}="card-text text-muted">Get support assistance</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer {class_attr}="bg-dark text-white py-5 mt-5">
        <div {class_attr}="container">
            <div {class_attr}="row g-4">
                <div {class_attr}="col-md-4">
                    <h5 {class_attr}="text-success mb-3">About Us</h5>
                    <p {class_attr}="text-white-50">Department committed to improving quality of life through sustainable development programs.</p>
                </div>
                <div {class_attr}="col-md-4">
                    <h5 {class_attr}="text-success mb-3">Quick Links</h5>
                    <ul {class_attr}="list-unstyled">
                        <li><a href="#" {class_attr}="text-white-50 text-decoration-none">About Department</a></li>
                        <li><a href="#" {class_attr}="text-white-50 text-decoration-none">Programs</a></li>
                        <li><a href="#" {class_attr}="text-white-50 text-decoration-none">Resources</a></li>
                    </ul>
                </div>
                <div {class_attr}="col-md-4">
                    <h5 {class_attr}="text-success mb-3">Contact</h5>
                    <p {class_attr}="text-white-50 mb-1">Email: info@department.gov.in</p>
                    <p {class_attr}="text-white-50 mb-0">Phone: 1800-XXX-XXXX</p>
                </div>
            </div>
            <hr {class_attr}="border-secondary my-4">
            <div {class_attr}="text-center">
                <p {class_attr}="text-white-50 mb-0">© 2026 Department, Government of India. All Rights Reserved.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/js/ux4g.bundle.min.js"></script>
</body>
</html>'''
