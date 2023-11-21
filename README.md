# Nanosatellite-Telemetry-Telecommand-and-Data-Visualization

## Design and Implementation of a Web-Based App for Nanosatellite Telemetry, Telecommand and Data Visualization 

### Description
This capstone project is a comprehensive endeavor aimed at developing a modular, reusable, and user-friendly web application to streamline satellite mission control and management. It provides mission operators with the capability to efficiently send telecommands to the spacecraft and process, log, and visualize data received.

### Scope   
- **Target**: One control station and only one satellite to control.
- **Mission Management Activities**:
  - Send telemetry, mission data requests, and telecommand to spacecraft.
  - Receive telemetry/ mission data requested and telecommand ACK.
  - Asynchronous mission management via predefined plans are out of scope.
  - Activities related to satellite tracking and ground station hardware control are outside the scope.

### Key Features  
#### Functional Requirements:
- Send/receive telecommands and telemetry/mission data (images) requests.
- Manage mission control activities pre-pass, during satellite pass, and post pass.
- Log all mission events, housekeeping data per subsystem, mission data and satellite future passes in a database.
- Provide a user-friendly interface for data visualization and mission operations.

#### Quality Attributes (Non-functional Requirements)
- **Modularity**: Separate/self-contained modules per satellite subsystem (OBC, EPS, COM, ADCS, Payload). Interaction between modules through well-defined uniform interfaces.
- **Extensibility**: Ability to accommodate new features/functionalities with minimal changes to the existing codebase.
- **Security**: The app should protect data and resources from unauthorized access and security threats (using, for example, authentication; authorization, etc.)
- **User-friendliness**: Easy to use.
- **Portability**: The app should be platform-independent (cross-platform compatibility).
- **Robustness**: The app should have minimal handling of unexpected inputs and situations for graceful management without crashing or causing data corruption.
