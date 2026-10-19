body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, #101826 0%, #1d2a39 100%);
  color: #e7f0ff;
}

.app-shell {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 16px 48px;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #7fe7c9;
  font-size: 11px;
}

h1, h2 {
  margin: 0 0 12px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.card {
  background: rgba(14, 22, 33, 0.8);
  border: 1px solid rgba(127, 231, 201, 0.25);
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 12px 38px rgba(0,0,0,0.15);
}

.full-width {
  margin-top: 16px;
}

label {
  display: block;
  margin: 12px 0;
  font-weight: 600;
}

input, button {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #35536d;
  background: #0d1726;
  color: white;
  font-size: 15px;
}

button {
  margin-top: 8px;
  background: linear-gradient(135deg, #2c8f72, #43c59e);
  border: none;
  font-weight: 700;
  cursor: pointer;
}

.status-pill {
  background: #1f6b62;
  border: 1px solid #91dbc5;
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.output-box {
  margin-top: 16px;
  background: rgba(12, 25, 38, 0.9);
  border: 1px solid rgba(127, 231, 201, 0.2);
  border-radius: 12px;
  padding: 12px;
  min-height: 80px;
  line-height: 1.6;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border-bottom: 1px solid rgba(127, 231, 201, 0.15);
  padding: 12px 8px;
  text-align: left;
}

@media (max-width: 540px) {
  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }
}
