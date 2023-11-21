// React core
import { useState } from "react";
import axios from "axios"; // for API requests

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

function OBC() {
  const [selectedCommand, setSelectedCommand] = useState(null);
  const [selectedTelemetryRequest, setSelectedTelemetryRequest] =
    useState(null);
  const [actionLog, setActionLog] = useState([]);

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
  ];

  const telemetryRequests = [
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

  // Preset Telemetry Requests
  const presetTelemetryRequests = [
    { name: "Get Housekeeping", command: "obc_telem_hk_get_cb" },
    { name: "Get Telemetry CMD", command: "obc_telem_hk_cmd_get_cb" },
    { name: "Get Persistent HK", command: "obc_telem_hk_persist_get_cb" },
  ];

  const handleSendCommand = async (command) => {
    try {
      const response = await axios.post(
        "http://" + window.location.hostname + ":8000/obc",
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

  const handleSendTelemetryRequest = async (request) => {
    try {
      const response = await axios.post(
        "http://" + window.location.hostname + ":8000/obc",
        {
          request,
        }
      );
      logAction(
        `${request} sent successfully. Response: ${JSON.stringify(
          response.data
        )}`
      );
    } catch (error) {
      logAction(`Error sending ${request}: ${error}`);
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
                      {telemetryRequests.map((request, index) => (
                        <ListItem key={index} disablePadding>
                          <ListItemButton
                            selected={
                              selectedTelemetryRequest === request.command
                            }
                            onClick={() =>
                              setSelectedTelemetryRequest(request.command)
                            }
                          >
                            <ListItemText primary={request.name} />
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

export default OBC;
