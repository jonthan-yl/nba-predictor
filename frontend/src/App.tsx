import { useEffect, useState } from "react";
import ProjectionTable from "./components/ProjectionTable";

type Projection = {
    player_id: number;
    name: string;
    minutes: number;
    points: number;
    rebounds: number;
    assists: number;
};

function App() {
  const [data, setData] = useState<Projection[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("/api/projections/today")
      .then((res) => {
        if (!res.ok) throw new Error("Request failed");
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading projections…</div>;
  if (error) return <div>Error loading projections</div>;

  return (
    <div style={{ padding: "2rem" }}>
      <h2>NBA Projections (Today)</h2>
      <ProjectionTable projections={data} />
    </div>
  );
}

export default App;
