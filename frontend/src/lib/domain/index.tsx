import DomainCreate from "./Create";
import BlurLinearIcon from "@mui/icons-material/BlurLinear";
import DomainEdit from "./Edit";
import DomainList from "./List";
import PostList from "../report/PostList";

const domain = {
  edit: DomainEdit,
  create: DomainCreate,
  list: DomainList,
  // show: PostList,
  icon: BlurLinearIcon,
  options: { label: "推广网址" },
};

export default domain;
