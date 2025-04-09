from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import StringMemory
import logging
from linkedin_utils import create_linkedin_client

# Set up logging for LinkedIn operations
logger = logging.getLogger(__name__)
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AiLinkedinNewsletter():
	"""AiLinkedinNewsletter crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True
		)
	
	@agent
	def newsletter_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['newsletter_writer'],
			verbose=True
		)
    
	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			verbose=True
		)

	@agent
	def linkedin_poster(self) -> Agent:  # New agent for LinkedIn posting
		return Agent(
			config=self.agents_config['linkedin_poster'],
			verbose=True
		)

	

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def draft_newsletter_task(self) -> Task:
		return Task(
			config=self.tasks_config['draft_newsletter_task'],
		)

	@task
	def review_newsletter_task(self) -> Task:
		return Task(
			config=self.tasks_config['review_newsletter_task'],
			output_file='newsletter.md'
		)

	@task
	def post_newsletter_task(self) -> Task:  # New task for LinkedIn posting
		return Task(
			config=self.tasks_config['post_newsletter_task'],
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the AiLinkedinNewsletter crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		# Create a memory source with LinkedIn best practices
		linkedin_best_practices = StringMemory(
			"""
			LinkedIn Post Best Practices:
			1. Keep posts under 3,000 characters for optimal engagement
			2. Use 3-5 relevant hashtags
			3. Include a clear call-to-action
			4. Break content into digestible paragraphs
			5. Mention relevant companies or individuals with @mentions
			6. Include a compelling hook in the first 2-3 lines
			"""
		)

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			knowledge_sources=[linkedin_best_practices],
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

	def _handle_linkedin_post_error(self, error):
		"""Handle errors that occur during LinkedIn posting"""
		logger.error(f"LinkedIn posting error: {str(error)}")
		# Additional error handling logic like notifications or fallback
		return {"status": "error", "message": str(error)}
