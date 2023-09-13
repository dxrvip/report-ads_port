import * as React from "react";
import {
  BooleanField,
  useTranslate,
  TextField,
  ShowBase,
  UrlField,
  DateField,
  Labeled,
} from "react-admin";
import { Box, Stack, Typography, IconButton } from "@mui/material";
import { Card } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
// const TextUirl = () => {
//   const record = useRecordContext<any>();
//   console.log(record);
//   if (!record) return null;

//   return (
//     <Box
//       sx={{ textAlign: "left" }}
//       fontSize={12}
//       overflow={"hidden"}
//       whiteSpace={"nowrap"}
//     >
//       <Typography>{record.url}</Typography>
//     </Box>
//   );
// };

const ReviewEdit = (props: any) => {
//   const translate = useTranslate();
  return (
    <ShowBase resource="report" {...props}>
      <Box p={1} pt={5} width={{ xs: "100vW", sm: 400 }} mt={{ xs: 2, sm: 1 }}>
        <Stack direction="row" p={2}>
          <Typography variant="h6" flex="1">
            详细信息
          </Typography>
          <IconButton size="small">
            <CloseIcon />
          </IconButton>
        </Stack>
        <Card>
          <Stack direction="row" p={2} spacing={4}>
            <Labeled label="ID:">
              <TextField source="id" />
            </Labeled>
            <Labeled label="文章Id">
              <TextField source="post.id" />
            </Labeled>
            <Labeled label="访问时间:">
              <DateField showTime source="create" />
            </Labeled>
          </Stack>
          <Stack direction="column" p={2} pt={0}>
            <Labeled label="访问Ip">
              <TextField source="visitor.ip" />
            </Labeled>
            <Labeled label="文章slug">
              <TextField source="post.slug" />
            </Labeled>
            <Labeled label="进入Url:">
              <UrlField source="url" />
            </Labeled>
            <Labeled label="翻页">
              <BooleanField source="is_page" />
            </Labeled>
          </Stack>
          {/* 浏览器信息 */}
          <Stack direction="row" p={2} pt={0}>
            <Labeled label="指纹ID：">
              <TextField source="browser_info.fingerprint_id" />
            </Labeled>
          </Stack>
          <Stack direction="row" p={2} pt="0" spacing={4}>
            <Labeled label="浏览器">
              <TextField source="browser_info.equipment.browser" />
            </Labeled>
            <Labeled label="设备">
              <TextField source="browser_info.equipment.device" />
            </Labeled>
          </Stack>
          {/* "taboola信息" */}
          <Stack direction="row" p={2} pt="0" spacing={4}>
            <Labeled label="campaign_id">
              <TextField source="taboola_info.campaign_id" />
            </Labeled>
            <Labeled label="site_id">
              <TextField source="taboola_info.site_id" />
            </Labeled>
            <Labeled label="平台">
              <TextField source="taboola_info.platform" />
            </Labeled>
          </Stack>
        </Card>
      </Box>
    </ShowBase>
  );
};

export default ReviewEdit;
