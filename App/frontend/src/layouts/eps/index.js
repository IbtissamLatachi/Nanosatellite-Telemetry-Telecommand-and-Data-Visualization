// React core
import { useState } from "react";
import axios from "axios";

// @mui material components
import Divider from "@mui/material/Divider";
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

// Material Dashboard 2 React components
import MDBox from "components/MDBox";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";

function EPS() {
  const [selectedCommand, setSelectedCommand] = useState(null);
  const [selectedTelemetryRequest, setSelectedTelemetryRequest] =
    useState(null);
  const [actionLog, setActionLog] = useState([]);

  // Commands and Telemetry Requests
  const telecommands = [
    { name: "Get Config 1", command: "eps_cmd_get_config1_cb" },
    { name: "Set Config 1", command: "eps_cmd_set_config1_cb" },
    { name: "Get Config 2", command: "eps_cmd_get_config2_cb" },
    { name: "Set Config 2", command: "eps_cmd_set_config2_cb" },
    { name: "Get Config 3", command: "eps_cmd_get_config3_cb" },
    { name: "Set Config 3", command: "eps_cmd_set_config3_cb" },
    { name: "Set Timeout", command: "eps_cmd_set_timeout_cb" },
    { name: "Set Heater Control", command: "eps_cmd_set_heater_ctrl_cb" },
    { name: "Reset Watchdog Ground", command: "eps_cmd_reset_wdt_gnd_cb" },
    { name: "Set PPT Mode", command: "eps_cmd_set_pptmode_cb" },
    { name: "Set VBoost", command: "eps_cmd_set_vboost_cb" },
  ];

  const telemetryRequests = [
    { name: "Get Housekeeping", command: "eps_telem_hk_get_cb" },
    { name: "Get Persistent HK", command: "eps_telem_hk_persist_get_cb" },
  ];

  // Preset Telecommands
  const presetCommands = [
    { name: "Get Config 1", command: "eps_cmd_get_config1_cb" },
    { name: "Get Config 2", command: "eps_cmd_get_config2_cb" },
    { name: "Get Config 3", command: "eps_cmd_get_config3_cb" },
    { name: "Reset Watchdog Ground", command: "eps_cmd_reset_wdt_gnd_cb" },
  ];

  // Preset Telemetry Requests
  const presetTelemetryRequests = [
    { name: "Get Housekeeping", command: "eps_telem_hk_get_cb" },
    { name: "Get Persistent HK", command: "eps_telem_hk_persist_get_cb" },
  ];

  const handleSendCommand = async (command) => {
    try {
      const response = await axios.post(
        "http://" + window.location.hostname + ":8000/eps",
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

  const handleSendTelemetryRequest = async (command) => {
    try {
      const response = await axios.post(
        "http://" + window.location.hostname + ":8000/eps",
        {
          command,
        }
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

  // Function to log actions with a timestamp
  const logAction = (action) => {
    const timestamp = new Date().toLocaleTimeString();
    setActionLog((prevLog) => [...prevLog, `${timestamp} ${action}`]);
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12} md={8}>
            <Card>
              <MDBox p={3}>
                {/* Telecommand List with Scrollable View */}
                <Typography variant="h6">Telecommands</Typography>
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
                  <Box
                    display="flex"
                    flexDirection="column"
                    alignItems="flex-start"
                  >
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => handleSendCommand(selectedCommand)}
                      disabled={!selectedCommand}
                      sx={{
                        mb: 1,
                        width: "200px",
                        color: "common.black",
                        backgroundColor: "grey.300",
                        "&:hover": { backgroundColor: "primary.main" },
                      }}
                    >
                      Send Telecommand
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

                {/* Divider between categories */}
                <MDBox mt={4} mb={2}>
                  <Divider />
                </MDBox>

                {/* Telemetry Request List with Scrollable View */}
                <Typography variant="h6">Telemetry Requests</Typography>
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
                      {telemetryRequests.map((command, index) => (
                        <ListItem key={index} disablePadding>
                          <ListItemButton
                            selected={
                              selectedTelemetryRequest === command.command
                            }
                            onClick={() =>
                              setSelectedTelemetryRequest(command.command)
                            }
                          >
                            <ListItemText primary={command.name} />
                          </ListItemButton>
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                  <Box
                    display="flex"
                    flexDirection="column"
                    alignItems="flex-start"
                  >
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() =>
                        handleSendTelemetryRequest(selectedTelemetryRequest)
                      }
                      disabled={!selectedTelemetryRequest}
                      sx={{
                        mb: 1,
                        width: "200px",
                        color: "common.black",
                        backgroundColor: "grey.300",
                        "&:hover": { backgroundColor: "primary.main" },
                      }}
                    >
                      Send Request
                    </Button>
                    {presetTelemetryRequests.map((presetRequest, index) => (
                      <Button
                        key={index}
                        variant="contained"
                        color="secondary"
                        onClick={() =>
                          handleSendTelemetryRequest(presetRequest.command)
                        }
                        sx={{
                          mb: 1,
                          width: "200px",
                          color: "common.black",
                          backgroundColor: "green.300",
                          "&:hover": { backgroundColor: "primary.main" },
                        }}
                      >
                        {presetRequest.name}
                      </Button>
                    ))}
                  </Box>
                </Box>
              </MDBox>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            {/* Action Log Window */}
            <Card>
              <MDBox p={2} sx={{ height: "600px", overflow: "auto" }}>
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

export default EPS;
