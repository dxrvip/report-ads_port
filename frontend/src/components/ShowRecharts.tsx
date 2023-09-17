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
import React from "react";
import SimpleDialog from "./SimpleDialog";
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
  const [open, setOpen] = React.useState(false);
  useEffect(() => {
    dataProvider
      .getOne(`list/${props?.type}`, { id: record.id })
      .then((response) => {
        setData(response.data);
      });
  }, []);
  if (!record) return null;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = (value: string) => {
    setOpen(false);
  };



  return data ? (
    <>
      <Grid item ml={6}>
        <Grid container justifyContent="left" spacing={2}>
          {Object.keys(data?.total as any).map((key, index) => (
            <Grid key={index} onClick={()=> {if(key=='Taboola') handleClickOpen()}} item>
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
              dataKey="bsum"
              name="访客"
              stroke="#e51b1b"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="psum"
              name="纵深数"
              stroke="#8884d8"
              fillOpacity={1}
              fill="url(#colorUv)"
            />
            <Area
              type="monotone"
              dataKey="rsum"
              name="浏览量"
              stroke="#82ca9d"
              fillOpacity={1}
              fill="url(#colorPv)"
            />
            <Area
              type="monotone"
              dataKey="tsum"
              name="Taboola"
              stroke="#2d2929"
              fillOpacity={1}
              fill="url(#colorPv)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </Grid>
      <SimpleDialog open={open} onClose={handleClose} />
    </>
  ) : null;
};

export default CustomerField;
