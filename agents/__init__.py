class Agent:
    """Base class for all automated agents"""
    def __init__(self, name: str, purpose: str):
        self.name = name
        self.purpose = purpose

    def perform_task(self, task: str) -> str:
        """Perform a generic task. Subclasses should override."""
        return f"{self.name} executed task: {task}"


class ProjectManagerAgent(Agent):
    """Coordinates project planning and overall management"""
    def __init__(self):
        super().__init__("ProjectManager", "Oversee project planning and coordination")


class ArchitectAgent(Agent):
    """Designs system architecture and technology choices"""
    def __init__(self):
        super().__init__("Architect", "Design system architecture")


class DeveloperAgent(Agent):
    """Implements features and fixes bugs"""
    def __init__(self):
        super().__init__("Developer", "Implement features")


class QAAgent(Agent):
    """Responsible for testing and quality assurance"""
    def __init__(self):
        super().__init__("QA", "Quality assurance and testing")


class DevOpsAgent(Agent):
    """Handles deployment and infrastructure"""
    def __init__(self):
        super().__init__("DevOps", "Deployment and infrastructure automation")


class ReviewAgent(Agent):
    """Reviews code for quality and correctness"""
    def __init__(self):
        super().__init__("Reviewer", "Code review and approval")


class DocumentationAgent(Agent):
    """Generates and maintains documentation"""
    def __init__(self):
        super().__init__("Documentation", "Create project documentation")


class SecurityAgent(Agent):
    """Checks security and performs audits"""
    def __init__(self):
        super().__init__("Security", "Perform security audits")


class MaintenanceAgent(Agent):
    """Keeps projects up to date and running smoothly"""
    def __init__(self):
        super().__init__("Maintenance", "Routine maintenance tasks")


class DataAnalysisAgent(Agent):
    """Analyzes data and generates reports"""
    def __init__(self):
        super().__init__("DataAnalysis", "Data processing and analysis")


def list_default_agents():
    """Return instances of all default agents"""
    return [
        ProjectManagerAgent(),
        ArchitectAgent(),
        DeveloperAgent(),
        QAAgent(),
        DevOpsAgent(),
        ReviewAgent(),
        DocumentationAgent(),
        SecurityAgent(),
        MaintenanceAgent(),
        DataAnalysisAgent(),
    ]
