import { type Projection } from "../Types/Projection";

type Props = {
  projections: Projection[];
};

function ProjectionTable({ projections }: Props) {
  if (projections.length === 0) {
    return <div>No projections available</div>;
  }

  return (
    <table style={{ borderCollapse: "collapse", width: "100%" }}>
      <thead>
        <tr>
          <th style={th}>Player</th>
          <th style={th}>Min</th>
          <th style={th}>Pts</th>
          <th style={th}>Reb</th>
          <th style={th}>Ast</th>
        </tr>
      </thead>
      <tbody>
        {projections.map((p) => (
          <tr key={p.player_id}>
            <td style={td}>{p.name}</td>
            <td style={td}>{p.minutes.toFixed(1)}</td>
            <td style={td}>{p.points.toFixed(1)}</td>
            <td style={td}>{p.rebounds.toFixed(1)}</td>
            <td style={td}>{p.assists.toFixed(1)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const th: React.CSSProperties = {
  borderBottom: "1px solid #ddd",
  textAlign: "left",
  padding: "8px",
};

const td: React.CSSProperties = {
  padding: "8px",
  borderBottom: "1px solid #eee",
};

export default ProjectionTable;
