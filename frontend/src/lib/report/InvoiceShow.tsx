// import * as React from "react";
import { Box, Card, CardContent, Grid, Typography, Paper } from "@mui/material";
import { useDataProvider, useRecordContext } from "react-admin";
// import { makeStyles, Theme, createStyles } from "@mui/material/styles";
import { Customer, Invoice } from "../../types";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
  ResponsiveContainer
} from "recharts";
import { useEffect, useState } from "react";

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

const CustomerField = () => {
  const record = useRecordContext<Customer>();
  const dataProvider = useDataProvider();
  const [data, setData] = useState<Data>();
  useEffect(() => {
    dataProvider.getOne("list/post", { id: record.id }).then((response) => {
      console.log(response);
      setData(response.data);
    });
  }, []);

  // const data = [
  //   {
  //     name: 'Page A',
  //     uv: 4000,
  //     pv: 2400,
  //     amt: 2400,
  //   },
  //   {
  //     name: 'Page B',
  //     uv: 3000,
  //     pv: 1398,
  //     amt: 2210,
  //   },
  //   {
  //     name: 'Page C',
  //     uv: 2000,
  //     pv: 9800,
  //     amt: 2290,
  //   },
  //   {
  //     name: 'Page D',
  //     uv: 2780,
  //     pv: 3908,
  //     amt: 2000,
  //   },
  //   {
  //     name: 'Page E',
  //     uv: 1890,
  //     pv: 4800,
  //     amt: 2181,
  //   },
  //   {
  //     name: 'Page F',
  //     uv: 2390,
  //     pv: 3800,
  //     amt: 2500,
  //   },
  //   {
  //     name: 'Page G',
  //     uv: 3490,
  //     pv: 4300,
  //     amt: 2100,
  //   },
  // ];

  return data ? (
    <>
      <Grid item ml={4}>
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
      <Grid mt={4}>
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
              dataKey="bsum"
              name="UV"
              stroke="#8884d8"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="psum"
              name="翻页数"
              stroke="#8884d8"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="rsum"
              name="PV"
              stroke="#82ca9d"
              fillOpacity={1}
              fill="url(#colorPv)"
            />
            <Area
              type="monotone"
              dataKey="tsum"
              name="Taboola"
              stroke="#82ca9d"
              fillOpacity={1}
              fill="url(#colorPv)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </Grid>
    </>
  ) : null;
};

const InvoiceShow = () => {
  const record = useRecordContext<Invoice>();

  if (!record) return null;
  return (
    <Card sx={{ width: "98%", margin: "auto" }}>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography gutterBottom>
              Id: ({record.id}) -
              <a style={{ marginLeft: "40px" }} href={record.url}>
                {record.url}
              </a>
            </Typography>
          </Grid>
        </Grid>
        <Grid
          container
          direction="row"
          justifyContent="flex-start"
          alignItems="center"
        ></Grid>

        <Box margin="10px 0">
          <CustomerField />
        </Box>
      </CardContent>
    </Card>
  );
};

export default InvoiceShow;
