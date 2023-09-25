import { Grid, Typography, Paper } from "@mui/material";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
  ResponsiveContainer,
} from "recharts";
import { useEffect, useState } from "react";
import { useDataProvider, useRecordContext } from "react-admin";
import { Customer } from "../types";
interface Result {
  bsum: Number;
  rsum: Number;
  psum: Number;
  tsum: Number;
  date: string;
}
type Data = {
  result: Array<Result>;
  total: { 翻页?: number; PV: number; UV: number; Taboola: number };
};

const CustomerField = (props: any) => {
  const record = useRecordContext<Customer>();
  const dataProvider = useDataProvider();
  const [data, setData] = useState<Data>();
  useEffect(() => {
    dataProvider
      .getOne(`list/${props?.type}`, { id: record.id })
      .then((response) => {
        setData(response.data);
      });
  }, [props, record]);
  if (!record) return null;

  return data ? (
    <>
      <Grid item ml={6}>
        <Grid container justifyContent="left" spacing={2}>
          {Object.keys(data?.total as any).map((key, index) => (
            <Grid key={index} item>
              <Paper
                elevation={0}
                sx={{
                  width: "70px",
                  height: "70px",
                  backgroundColor: "wheat",
                  textAlign: "center",
                  lineHeight: "30px",
                  fontSize: "2em",
                  padding: "4px",
                  position: "relative",
                }}
              >
                <Typography sx={{ fontSize: "12px", display: "p" }}>
                  {key}
                </Typography>
                {(data as any).total[key]}
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Grid>
      <Grid item>
        <ResponsiveContainer width={830} minHeight={200}>
          <AreaChart
            data={data?.result}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#82ca9d" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="date" />
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="page_sum"
              name="翻页数"
              stroke="#ff0043"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="zs_sum"
              name="有纵深访客数"
              stroke="#ff00b2"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="taboola_count"
              name="Site_Id"
              stroke="#ff00e3"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="ads_count"
              name="广告点击数"
              stroke="#a100ff"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="borwser_count"
              name="指纹访客数"
              stroke="#2200ff"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="tab_open_sum"
              name="siteId进入数"
              stroke="#00bfff"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="ip_count"
              name="Ip访客数"
              stroke="#00ffbb"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="report_count"
              name="总浏览量"
              stroke="#00ff2e"
              fillOpacity={1}
              fill="url(#colorPv)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </Grid>
    </>
  ) : null;
};

export default CustomerField;
