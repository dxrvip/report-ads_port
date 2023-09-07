import DomainCreate from "./Create";
import BlurLinearIcon from "@mui/icons-material/BlurLinear";
import DomainEdit from "./Edit";
import DomainList from "./List";

const domain = {
  edit: DomainEdit,
  create: DomainCreate,
  list: DomainList,
  icon: BlurLinearIcon,
  options: { label: "数据记录" },
};

export default domain;
