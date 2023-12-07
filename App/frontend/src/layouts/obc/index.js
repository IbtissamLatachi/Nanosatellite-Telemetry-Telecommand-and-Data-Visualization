// React core
import { useState } from "react";
import axios from "axios";
import { useEffect } from "react";

// @mui material components
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemButton from "@mui/material/ListItemButton";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import IconButton from "@mui/material/IconButton";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import RemoveCircleOutlineIcon from "@mui/icons-material/RemoveCircleOutline";
import SendIcon from "@mui/icons-material/Send";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";

// Recharts
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
} from "recharts";

function OBC() {
  const [selectedCommand, setSelectedCommand] = useState(null);
  const [commandsToSend, setCommandsToSend] = useState([]);
  const [actionLog, setActionLog] = useState([]);
  const [checkedCategories, setCheckedCategories] = useState({
    EPS: true,
    COM: true,
    ADCS: true,
    CAM: true,
  });

  // Commands and Telemetry Requests
  const telecommands = [
    { name: "Get MASAT State", command: "obc_cmd_get_masat_state_cb" },
    { name: "Load Image", command: "obc_cmd_load_imag_cb" },
    { name: "Track Target", command: "obc_cmd_track_target_cb" },
    { name: "Sync OBC Time", command: "obc_cmd_timesync_cb" },
    { name: "Jump to RAM", command: "obc_cmd_jump_ram_cb" },
    { name: "Set Boot Config", command: "obc_cmd_boot_conf_cb" },
    { name: "Delete Config", command: "obc_cmd_conf_del_cb" },
    { name: "RAM to ROM", command: "obc_cmd_ram_to_rom_cb" },
    { name: "Get Boot Count", command: "obc_cmd_boot_count_get_cb" },
    { name: "Reset Boot Count", command: "obc_cmd_boot_count_reset_cb" },
    { name: "Get Housekeeping", command: "obc_telem_hk_get_cb" },
    { name: "Get Telemetry CMD", command: "obc_telem_hk_cmd_get_cb" },
    { name: "Get Persistent HK", command: "obc_telem_hk_persist_get_cb" },
  ];

  // Preset Telecommands
  const presetCommands = [
    { name: "Get MASAT State", command: "obc_cmd_get_masat_state_cb" },
    { name: "Sync OBC Time", command: "obc_cmd_timesync_cb" },
    { name: "Reset Boot Count", command: "obc_cmd_boot_count_reset_cb" },
  ];

  const handleSendCommand = async (command) => {
    try {
      const response = await axios.post(
        "http://" + window.location.hostname + ":8000/obc/command",
        { command }
      );
      logAction(
        `${command} sent successfully. Response: ${JSON.stringify(
          response.data
        )}`
      );
    } catch (error) {
      logAction(`Error sending ${command}: ${error}`);
    }
  };

  // Add or remove commands/telemetry from the list to send
  const modifyList = (item, listType, action) => {
    setActionLog((prevLog) => [
      ...prevLog,
      `${new Date().toLocaleTimeString()} ${
        action === "add" ? "Added" : "Removed"
      } ${item} to ${listType}`,
    ]);
    setCommandsToSend((prevList) =>
      action === "add"
        ? [...prevList, item]
        : prevList.filter((cmd) => cmd !== item)
    );
  };

  // Send all commands/telemetry requests
  const handleSendAll = async (listType) => {
    if (listType === "commands") {
      for (const command of commandsToSend) {
        await handleSendCommand(command);
      }
      setCommandsToSend([]);
    }
  };

  // Function to log actions with a timestamp
  const logAction = (action) => {
    const timestamp = new Date().toLocaleTimeString();
    setActionLog((prevLog) => [...prevLog, `${timestamp} ${action}`]);
  };

  const toggleCategory = (category) => {
    setCheckedCategories((prevCategories) => ({
      ...prevCategories,
      [category]: !prevCategories[category],
    }));
  };

  const [obcHousekeepingData, setObcHousekeepingData] = useState([]);
  const [obcCommandData, setObcCommandData] = useState([]);

  // Fetch OBC Housekeeping Data
  const fetchObcHousekeepingData = async () => {
    try {
      const response = await axios.get(
        "http://" + window.location.hostname + ":8000/obc/getHk"
      );
      setObcHousekeepingData(response.data.housekeeping_data);
    } catch (error) {
      console.error("Error fetching OBC Housekeeping Data:", error);
    }
  };

  // Fetch OBC Command Data
  const fetchObcCommandData = async () => {
    try {
      const response = await axios.get(
        "http://" + window.location.hostname + ":8000/obc/gettelem"
      );
      setObcCommandData(response.data.command_data);
    } catch (error) {
      console.error("Error fetching OBC Command Data:", error);
    }
  };

  useEffect(() => {
    fetchObcHousekeepingData();
    fetchObcCommandData();
  }, []);

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12} md={8}>
            <Card>
              <MDBox p={3}>
                {/* Telecommand List with Scrollable View */}
                <Typography variant="h6">
                  Telecommands & Telemetry Requests
                </Typography>
                <Box
                  display="flex"
                  justifyContent="space-between"
                  alignItems="flex-start"
                  mt={2}
                >
                  <Box
                    sx={{
                      width: "70%",
                      maxHeight: 200,
                      overflow: "auto",
                      mr: 2,
                      border: "1px solid lightgrey",
                      borderRadius: "4px",
                    }}
                  >
                    <List component={Paper}>
                      {telecommands.map((telecommand, index) => (
                        <ListItem key={index} disablePadding>
                          <ListItemButton
                            selected={selectedCommand === telecommand.command}
                            onClick={() =>
                              setSelectedCommand(telecommand.command)
                            }
                          >
                            <ListItemText primary={telecommand.name} />
                          </ListItemButton>
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                  <List component={Paper}>
                    {/* HERE SHOULD BE THE SCHEDULED COMMANDS BEFORE THEY ARE SENT YOU SHOULD BE ABLE TO ADD AND REMOVE THEM.*/}
                  </List>
                  <Box
                    display="flex"
                    flexDirection="column"
                    alignItems="flex-start"
                  >
                    <Button
                      variant="contained"
                      color="primary"
                      endIcon={<SendIcon />}
                      onClick={() => handleSendAll("commands")}
                      disabled={commandsToSend.length === 0}
                      sx={{
                        mb: 1,
                        width: "200px",
                        color: "common.black",
                        backgroundColor: "green.300",
                        "&:hover": { backgroundColor: "primary.main" },
                      }}
                    >
                      Send Command(s)
                    </Button>
                    {presetCommands.map((presetCommand, index) => (
                      <Button
                        key={index}
                        variant="contained"
                        color="secondary"
                        onClick={() => handleSendCommand(presetCommand.command)}
                        sx={{
                          mb: 1,
                          width: "200px",
                          color: "common.black",
                          backgroundColor: "green.300",
                          "&:hover": { backgroundColor: "primary.main" },
                        }}
                      >
                        {presetCommand.name}
                      </Button>
                    ))}
                  </Box>
                </Box>
                {/* Add the new + and - buttons */}
                <IconButton
                  color="primary"
                  onClick={() => modifyList(selectedCommand, "commands", "add")}
                  disabled={!selectedCommand}
                >
                  <AddCircleOutlineIcon />
                </IconButton>
                <IconButton
                  color="secondary"
                  onClick={() =>
                    modifyList(selectedCommand, "commands", "remove")
                  }
                  disabled={
                    !selectedCommand ||
                    !commandsToSend.includes(selectedCommand)
                  }
                >
                  <RemoveCircleOutlineIcon />
                </IconButton>
              </MDBox>
            </Card>
            <MDBox mt={4}>
              {/* OBC Housekeeping Data Visualization */}
              <Card>
                <MDBox p={3}>
                  <Typography variant="h6">OBC Housekeeping Data</Typography>
                  <LineChart
                    width={600}
                    height={300}
                    data={obcHousekeepingData}
                  >
                    {/* Line for Temperature */}
                    <Line
                      type="monotone"
                      dataKey="temperature"
                      stroke="#8884d8"
                    />
                    {/* Add other Lines for different data keys as needed */}
                    {/* Example: <Line type="monotone" dataKey="cpu_load" stroke="#82ca9d" /> */}
                    <CartesianGrid stroke="#ccc" />
                    <XAxis dataKey="timestamp" />
                    <YAxis />
                    <Tooltip />
                  </LineChart>
                </MDBox>
              </Card>
            </MDBox>

            <MDBox mt={4}>
              {/* OBC Command Data Visualization */}
              <Card>
                <MDBox p={3}>
                  <Typography variant="h6">OBC Command Data</Typography>
                  <BarChart width={600} height={300} data={obcCommandData}>
                    {/* Bar for Command Success Rate */}
                    <Bar dataKey="command_success_rate" fill="#82ca9d" />
                    {/* Add other Bars for different data keys as needed */}
                    {/* Example: <Bar dataKey="recent_errors" fill="#8884d8" /> */}
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" />
                    <YAxis />
                    <Tooltip />
                  </BarChart>
                </MDBox>
              </Card>
            </MDBox>
          </Grid>

          <Grid item xs={12} md={4}>
            {/* Filter checkboxes */}
            {/*
            <Box
              sx={{ display: "flex", flexDirection: "row", flexWrap: "wrap" }}
            >
              {Object.keys(checkedCategories).map((category) => (
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={checkedCategories[category]}
                      onChange={() => toggleCategory(category)}
                    />
                  }
                  label={category}
                  key={category}
                />
              ))}
            </Box>
                */}
            {/* Action Log Window */}
            <Card>
              <MDBox p={2} sx={{ height: "700px", overflow: "auto" }}>
                {actionLog.map((log, index) => (
                  <MDBox
                    key={index}
                    component="p"
                    m={0}
                    sx={{ fontSize: "0.875rem" }}
                  >
                    {log}
                  </MDBox>
                ))}
              </MDBox>
            </Card>
          </Grid>
        </Grid>
      </MDBox>
      <Footer />
    </DashboardLayout>
  );
}

export default OBC;
