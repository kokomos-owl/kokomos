# node_services.py
# Provides business logic and data services for node operations within the Raven system.

from datetime import datetime
from typing import Dict, Any
from neomodel import db
from models.base_models import BaseNode, AbstractNode
from exceptions import NodeValidationError
from utils.node_factory import NodeFactory  # Assuming NodeFactory is defined in base_nodes.py or a similar utility module

class NodeService:
    def __init__(self):
        # A dictionary to store node instances keyed by node ID might not be necessary if nodes are directly managed by Neo4j/Neomodel
        pass

    def add_node(self, node_data: Dict[str, Any]) -> str:
        """
        Adds a new node with the specified properties to the system.
        Utilizes the NodeFactory for instantiation to avoid duplicating factory functions.

        Args:
            node_data (Dict[str, Any]): A dictionary containing the properties of the node to be added, including the node type.

        Returns:
            str: The unique identifier for the newly added node.
        """
        try:
            node_type = node_data.pop('type')  # Extract the node type from the data
            node = NodeFactory.create_node(node_type, **node_data)  # Create node instance using the factory
            node.save()  # Save the node to the database
            return str(node.node_id)
        except Exception as e:
            raise NodeValidationError(f"Failed to add node: {e}")

    def update_node(self, node_id: str, update_data: Dict[str, Any]):
        """
        Updates the properties of an existing node.

        Args:
            node_id (str): The unique identifier of the node to update.
            update_data (Dict[str, Any]): A dictionary containing the properties to update on the node.
        """
        try:
            node = BaseNode.nodes.get(node_id=node_id)  # Retrieve the node by ID
            for key, value in update_data.items():
                setattr(node, key, value)
            node.save()
        except BaseNode.DoesNotExist:
            raise NodeValidationError(f"Node with ID {node_id} not found.")
        except Exception as e:
            raise NodeValidationError(f"Failed to update node: {e}")

    def delete_node(self, node_id: str):
        """
        Deletes a node from the system.

        Args:
            node_id (str): The unique identifier of the node to delete.
        """
        try:
            node = BaseNode.nodes.get(node_id=node_id)
            node.delete()  # This deletes the node from the database
        except BaseNode.DoesNotExist:
            raise NodeValidationError(f"Node with ID {node_id} not found.")
        except Exception as e:
            raise NodeValidationError(f"Failed to delete node: {e}")

    # Methods for logging interactions, integrating feedback, and tracking history can be adapted to leverage Neo4j's capabilities
    # and the structures defined in base_nodes.py, ensuring that all node-related operations are consistent with the system's design principles.

    # Additional methods and utilities as needed by your application logic...
    # Ensure thorough documentation for each method.
    # Implement unit tests for validation and reliability.