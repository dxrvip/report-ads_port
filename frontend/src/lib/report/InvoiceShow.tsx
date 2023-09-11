// import * as React from "react";
import { Box, Card, CardContent, Grid, Typography, Paper } from "@mui/material";
import { useDataProvider, useRecordContext } from "react-admin";
// import { makeStyles, Theme, createStyles } from "@mui/material/styles";
import { Customer, Invoice } from "../../types";
import { Area, AreaChart, CartesianGrid, Tooltip, XAxis, YAxis } from "recharts";
import { useEffect, useState } from "react";
const CustomerField = () => {
    const record = useRecordContext<Customer>();
    const dataProvider = useDataProvider();
    const [user, setUser] = useState();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState();
    useEffect(()=> {
        console.log(dataProvider);
        // dataProvider.getOne("list/post", {id: record.id})
    }, [])
    
    const data = [
      {
        name: 'Page A',
        uv: 4000,
        pv: 2400,
        amt: 2400,
      },
      {
        name: 'Page B',
        uv: 3000,
        pv: 1398,
        amt: 2210,
      },
      {
        name: 'Page C',
        uv: 2000,
        pv: 9800,
        amt: 2290,
      },
      {
        name: 'Page D',
        uv: 2780,
        pv: 3908,
        amt: 2000,
      },
      {
        name: 'Page E',
        uv: 1890,
        pv: 4800,
        amt: 2181,
      },
      {
        name: 'Page F',
        uv: 2390,
        pv: 3800,
        amt: 2500,
      },
      {
        name: 'Page G',
        uv: 3490,
        pv: 4300,
        amt: 2100,
      },
    ];
    
    return record ? (
      <AreaChart
        width={730}
        height={250}
        data={data}
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
        <XAxis dataKey="name" />
        <YAxis />
        <CartesianGrid strokeDasharray="3 3" />
        <Tooltip />
        <Area
          type="monotone"
          dataKey="uv"
          stroke="#8884d8"
          fillOpacity={1}
          fill="url(#colorUv)"
        />
        <Area
          type="monotone"
          dataKey="pv"
          stroke="#82ca9d"
          fillOpacity={1}
          fill="url(#colorPv)"
        />
      </AreaChart>
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
        >
          <Grid item xs={12}>
            <Grid container justifyContent="left" spacing={2}>
              {[0, 1, 2].map((value) => (
                <Grid key={value} item>
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
                      position: "relative"
                    }}
                  >
                    <Typography sx={{fontSize: "12px", "display": "p"}}>总访客</Typography>
                    {record.bsum}
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>

        <Box margin="10px 0">
            <CustomerField />
        </Box>
      </CardContent>
    </Card>
  );
};



export default InvoiceShow;
