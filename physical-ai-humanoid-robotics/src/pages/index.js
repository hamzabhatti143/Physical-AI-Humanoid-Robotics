import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HomepageFeatures from "@site/src/components/HomepageFeatures";

import Heading from "@theme/Heading";
import styles from "./index.module.css";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          Physical AI & Humanoid Robotics
        </Heading>
        <p className="hero__subtitle">
          Discover how AI moves beyond the screen and into the physical world.
          This program bridges the gap between the digital brain and the
          physical body, guiding students to apply intelligent systems on real
          and simulated humanoid robots.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro"
          >
            Start Reading
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />"
    >
      <HomepageHeader />
      <main>
        <section className="module-cards-section">
          <div className="container">
            <div className="row">
              <div className="col col--6 margin-bottom--lg">
                <Link to="/docs/module-1-ros2" className="card module-card">
                  <div className="card__header">
                    <h3>Module 1: The Robotic Nervous System (ROS 2)</h3>
                  </div>
                  <div className="card__body">
                    <p>
                      Weeks 3-5: Dive into ROS 2 fundamentals, nodes, topics,
                      services, actions, and building packages with Python
                      (rclpy) and URDF for humanoid robots.
                    </p>
                  </div>
                </Link>
              </div>
              <div className="col col--6 margin-bottom--lg">
                <Link
                  to="/docs/module-2-digital-twin"
                  className="card module-card"
                >
                  <div className="card__header">
                    <h3>Module 2: The Digital Twin (Gazebo & Unity)</h3>
                  </div>
                  <div className="card__body">
                    <p>
                      Weeks 6-7: Explore robot simulation with Gazebo, URDF/SDF
                      formats, physics, sensor simulation, and high-fidelity
                      rendering with Unity.
                    </p>
                  </div>
                </Link>
              </div>
              <div className="col col--6 margin-bottom--lg">
                <Link
                  to="/docs/module-3-nvidia-isaac"
                  className="card module-card"
                >
                  <div className="card__header">
                    <h3>Module 3: The AI-Robot Brain (NVIDIA Isaac)</h3>
                  </div>
                  <div className="card__body">
                    <p>
                      Weeks 8-10: Learn about Isaac SDK, Isaac Sim for
                      photorealistic simulation, synthetic data generation,
                      AI-powered perception, and Isaac ROS for VSLAM and
                      navigation.
                    </p>
                  </div>
                </Link>
              </div>
              <div className="col col--6 margin-bottom--lg">
                <Link to="/docs/module-4-vla" className="card module-card">
                  <div className="card__header">
                    <h3>Module 4: Vision-Language-Action (VLA)</h3>
                  </div>
                  <div className="card__body">
                    <p>
                      Weeks 11-13: Understand humanoid robot kinematics, bipedal
                      locomotion, natural HRI design, GPT integration, and using
                      LLMs for cognitive planning and voice-to-action.
                    </p>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </section>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
